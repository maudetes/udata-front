from collections import namedtuple
import unicodedata

from flask import abort, current_app, redirect, url_for

from udata.i18n import I18nBlueprint
from udata.models import Dataset, GeoZone, TERRITORY_DATASETS
from udata.sitemap import sitemap
from udata_front import theme

blueprint = I18nBlueprint('territories', __name__)


def dict_to_namedtuple(name, data):
    """Convert a `data` dict to a namedtuple.

    Useful for easy attribute access.
    """
    return namedtuple(name, data.keys())(**data)


@blueprint.route('/territories/', endpoint='home')
def render_home():
    if not current_app.config.get('ACTIVATE_TERRITORIES'):
        return abort(404)

    highest_level = current_app.config['HANDLED_LEVELS'][-1]
    regions = GeoZone.objects(level=highest_level)
    regions = sorted(
        regions,
        key=lambda zone: unicodedata.normalize('NFD', zone.name)
                                    .encode('ascii', 'ignore'))

    return theme.render('territories/home.html', **{
        'geojson': {
            'type': 'FeatureCollection',
            'features': [region.toGeoJSON() for region in regions]
        },
        'regions': regions
    })


@blueprint.route('/town/<code>/')
def redirect_town(code):
    """
    Legacy redirect now prefixed with `territories` + French name.
    """
    return redirect(url_for('territories.redirect_territory',
                            level='commune', code=code))


@blueprint.route('/territory/town/<code>/')
def redirect_town2(code):
    """
    Legacy redirect for French name and GeoIDs.
    """
    return redirect(url_for('territories.redirect_territory',
                            level='commune', code=code))


@blueprint.route('/territory/county/<code>/')
def redirect_county(code):
    """
    Legacy redirect for French name and GeoIDs.
    """
    return redirect(url_for('territories.redirect_territory',
                            level='departement', code=code))


@blueprint.route('/territory/region/<code>/')
def redirect_region(code):
    """
    Legacy redirect for French name and GeoIDs.
    """
    return redirect(url_for('territories.redirect_territory',
                            level='region', code=code))


@blueprint.route('/territories/<level>/<code>@latest/',
                 endpoint='redirect_territory')
def redirect_territory(level, code):
    """
    Implicit redirect given the INSEE code.

    Optimistically redirect to the latest valid/known INSEE code.
    """
    territory = GeoZone.objects.filter(
        code=code, level='fr:{level}'.format(level=level)).first()
    return redirect(url_for('territories.territory', territory=territory))


@blueprint.route('/territories/<territory:territory>/', endpoint='territory')
def render_territory(territory):
    if not current_app.config.get('ACTIVATE_TERRITORIES'):
        return abort(404)

    # Only display dynamic datasets for present territories.
    base_datasets = []
    DATASETS = TERRITORY_DATASETS[territory.level_code]
    base_dataset_classes = sorted(DATASETS.values(), key=lambda a: a.order)
    base_datasets = [
        base_dataset_class(territory)
        for base_dataset_class in base_dataset_classes
    ]
    territories = [territory]

    # Retrieve all datasets then split between those optionally owned
    # by an org for that zone and others. We need to know if the current
    # user has datasets for that zone in order to display a custom
    # message to ease the conversion.
    datasets = Dataset.objects(spatial__zones__in=territories).visible()
    # Retrieving datasets from old regions.
    territory_datasets = []
    other_datasets = []
    if datasets:
        for dataset in datasets:
            if (dataset.organization and
                    territory.id == dataset.organization.zone):
                territory_datasets.append(dataset)
            else:
                other_datasets.append(dataset)
    context = {
        'territory': territory,
        'base_datasets': base_datasets,
        'other_datasets': other_datasets,
        'territory_datasets': territory_datasets
    }
    template = 'territories/{level_name}.html'.format(
        level_name=territory.level_name)
    return theme.render(template, **context)


@sitemap.register_generator
def sitemap_urls():
    if current_app.config.get('ACTIVATE_TERRITORIES'):
        for level in current_app.config.get('HANDLED_LEVELS'):
            for territory in (GeoZone.objects(level=level)
                                     .only('id', 'code', 'validity', 'slug')):
                # Remove 'fr:' manually from the level.
                territory = dict_to_namedtuple(
                    'Territory', {
                        'level_name': level[3:],
                        'id': territory.id,
                        'code': territory.code,
                        'slug': territory.slug,
                        'validity': territory.validity
                    })
                yield ('territories.territory', {'territory': territory},
                       None, 'weekly', 0.5)
