<template>
  <div class="fr-container">
    <Stepper :steps="steps" :currentStep="2"/>
    <div class="fr-grid-row">
      <Sidemenu
        class="fr-col-12 fr-col-md-5"
        :buttonText="$t('Help')"
        :onRight="true"
        :fixed="true"
        :showBorder="false"
      >
        <template #title>
          <span class="fr-icon--sm fr-icon-question-line" aria-hidden="true"></span>
          {{ $t('Help') }}
        </template>
        <Accordion
          :title= "$t('Choose the right format')"
          :id="publishFileAccordionId"
          :state="state.files"
          :opened="true"
        >
          <div class="markdown fr-m-0">
            <p class="fr-m-0 fr-mb-1w">
              {{ $t("Formats should be :") }}
            </p>
            <ul>
              <li>{{ $t("open : an open format doesn't add technical specifications that restrict data use (i.e. using a paid software) ;") }}</li>
              <li>{{ $t("easily reusable : a format easily reusable implies that anybody or server can reuse easily the dataset ;") }}</li>
              <li>{{ $t("usable in an automated processing system : an automated processing system allows to make automatic operations, related to data exploitation (i.e. a CSV file is easily usable by an automated system unlike a PDF file).") }}</li>
            </ul>
          </div>
          <Well class="fr-mt-1w" v-if="fieldHasWarning('files')" color="orange-terre-battue">
            {{ getWarningText("files") }}
          </Well>
        </Accordion>
        <Accordion
          :title= "$t('Add documentation')"
          :id="addDescriptionAccordionId"
          :state="state.hasDocumentation"
        >
          <div class="markdown fr-m-0">
            <p class="fr-m-0 fr-mb-1w">
              {{ $t("The description of a file facilitates the reuse of data. It includes, among others:") }}
            </p>
            <ul>
              <li>{{ $t("a general description of the dataset ;") }}</li>
              <li>{{ $t("a description of the data production mode ;") }}</li>
              <li>{{ $t("a description of the data model ;") }}</li>
              <li>{{ $t("a description of the data schema ;") }}</li>
              <li>{{ $t("a description of the metadata ;") }}</li>
              <li>{{ $t("a description of major changes.") }}</li>
            </ul>
          </div>
          <Well class="fr-mt-1w" v-if="fieldHasWarning('hasDocumentation')" color="orange-terre-battue">
            {{ getWarningText("hasDocumentation") }}
          </Well>
        </Accordion>
      </Sidemenu>
      <div class="fr-col-12 fr-col-md-7">
        <Container>
          <Well
            color="blue-cumulus"
            weight="regular"
            class="fr-mb-2w"
          >
            <div class="fr-grid-row">
              <div class="fr-col-auto fr-mr-3v">
                <img :src="editIcon" alt="" />
              </div>
              <div class="fr-col">
                <p class="fr-m-0 fr-text--bold">{{ $t('What is a file?') }}</p>
                <p class="fr-m-0 fr-text--xs">{{ $t('A dataset can contain multiple types of files (updates, history, documentation, source code, API, link, etc.)') }}</p>
              </div>
            </div>
          </Well>
          <fieldset class="fr-fieldset min-width-0" aria-labelledby="description-legend">
            <legend class="fr-fieldset__legend" id="description-legend">
              <h2 class="subtitle subtitle--uppercase fr-mb-3v">
                {{ $t("Files") }}
              </h2>
            </legend>
            <LinkedToAccordion
              class="fr-fieldset__element min-width-0"
              :accordion="publishFileAccordionId"
              @blur="touch"
            >
              <Container
                color="alt-grey"
                class="fr-grid-row fr-grid-row--middle flex-direction-column"
                v-if="files.length === 0"
              >
                <h3 class="fr-text--md fr-text--bold fr-m-0 fr-mb-2w">{{ $t("Add your first files") }}</h3>
                <UploadModalButton
                  groupClass="fr-grid-row flex-direction-column fr-grid-row--middle"
                  :label="$t('Add files')"
                  :title="$t('Add files (opens a modal dialog)')"
                  :multiple="true"
                  :required="true"
                  :hasError="fieldHasError('files')"
                  :errorText="getErrorText('files')"
                  @change="addFiles"
                />
              </Container>
              <template v-else>
                  <FileCard
                    v-for="(resource, index) in files"
                    class="fr-mb-3v"
                    :file="resource"
                    @delete="removeFile(index)"
                    @edit="$emit('editFile', files, index)"
                  />
                <div class="fr-grid-row fr-grid-row--center">
                  <ButtonLoader :width="114" v-if="loading"/>
                  <UploadModalButton
                    :label="$t('Add files')"
                    :title="$t('Add files (opens a modal dialog)')"
                    :multiple="true"
                    :required="true"
                    :hasError="fieldHasError('files')"
                    :errorText="getErrorText('files')"
                    @change="addFiles"
                    v-else
                  />
                </div>
              </template>
            </LinkedToAccordion>
          </fieldset>
          <Alert type="error" v-if="errors.length" class="fr-mt-n2w fr-mb-2w">
            <template #title>{{ $t("An error occured | Some errors occured", errors.length) }}</template>
            <ul v-if="errors.length > 1">
              <li v-for="error in errors">{{ error }}</li>
            </ul>
            <p v-else> {{ errors[0] }}</p>
          </Alert>
          <div class="fr-grid-row fr-grid-row--right">
            <ButtonLoader :width="66" v-if="loading"/>
            <button class="fr-btn" @click="submit" v-else>
              {{ $t("Next") }}
            </button>
          </div>
        </Container>
      </div>
    </div>
  </div>
</template>
<script>
import { computed, defineComponent, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import Accordion from '../../components/Accordion/Accordion.vue';
import AccordionGroup from '../../components/Accordion/AccordionGroup.vue';
import Alert from '../../components/Alert/Alert.vue';
import ButtonLoader from '../../components/Form/ButtonLoader.vue';
import Container from '../../components/Ui/Container/Container.vue';
import InputGroup from '../../components/Form/InputGroup/InputGroup.vue';
import FileCard from '../../components/Form/FileCard/FileCard.vue';
import LinkedToAccordion from '../../components/Form/LinkedToAccordion/LinkedToAccordion.vue';
import Sidemenu from '../../components/Sidemenu/Sidemenu.vue';
import Stepper from '../../components/Form/Stepper/Stepper.vue';
import UploadModalButton from '../../components/Form/UploadGroup/UploadModalButton.vue';
import Well from "../../components/Ui/Well/Well.vue";
import useUid from "../../composables/useUid";
import useFunctionalState from '../../composables/form/useFunctionalState';
import { requiredWithCustomMessage, withMessage } from '../../i18n';
import editIcon from "svg/illustrations/edit.svg";
import { isClosedFormat } from '../../helpers';
import { isLoading, isLoaded } from "../../api/resources";

export default defineComponent({
  components: { Accordion, AccordionGroup, Alert, ButtonLoader, Container, FileCard, InputGroup, LinkedToAccordion, Sidemenu, Stepper, UploadModalButton, Well, },
  emits: ["editFile", "next"],
  props: {
    errors: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    steps: {
      type: Array,
      required: true,
    },
    originalFiles: {
      /** @type {import("vue").PropType<Readonly<Array<import("../../types").NewDatasetFile>>>} */
      type: Array,
      required: true,
    }
  },
  setup(props, { emit }) {
    const { t } = useI18n();
    const { id: publishFileAccordionId } = useUid("accordion");
    const { id: addDescriptionAccordionId } = useUid("accordion");

    const files = ref([...props.originalFiles]);

    const fileRequired = requiredWithCustomMessage(t("At least one file is required."));

    /**
     * Validates that the dataset contains an open format file.
     * @param {Array<import("../../types").DatasetFile>} value
     */
    const onefileHasOpenFormats = (value) => value.reduce((previous, current) => previous || !isClosedFormat(current.format), false);

    /**
     * Validates that the dataset contains a documentation file.
     * @param {undefined} value
     * * @param {{files: Array<import("../../types").DatasetFile>}} siblings
     */
     const hasDocumentation = (value, siblings) => siblings.files.reduce((previous, current) => previous || current.type === "documentation" || !!current.description?.trim(), false);

    const requiredRules = {
      files: { fileRequired },
    };

    const warningRules = {
      files: { fileRequired, openFormat: withMessage(t("You did not add a file with an open format."), onefileHasOpenFormats) },
      hasDocumentation: { hasDocumentation: withMessage(t("You have not added a documentation file or described your files."), hasDocumentation) }
    };

    const { getErrorText, getFunctionalState, getWarningText, hasError, hasWarning, validateRequiredRules, v$, vWarning$ } = useFunctionalState({ files }, requiredRules, warningRules);

    /**
     *
     * @param {Array<import("../../types").NewDatasetFile>} newFiles
     */
    const addFiles = (newFiles) => {
      files.value.push(...newFiles);
      if(newFiles.length === 1 && newFiles[0].filetype === "remote") {
        emit('editFile', files, files.value.length - 1);
      }
    };

    /**
     *
     * @param {number} position
     */
    const removeFile = (position) => files.value.splice(position, 1);

    /**
     * @type {import("vue").ComputedRef<Record<string, import("../../types").AccordionFunctionalState>>}
     */
    const state = computed(() => {
      return {
        files: getFunctionalState(vWarning$.value.files.$dirty, v$.value.files.$invalid, vWarning$.value.files.$error),
        hasDocumentation: getFunctionalState(vWarning$.value.hasDocumentation.$dirty, false, vWarning$.value.hasDocumentation.$error),
      };
    });

    const touch = () => {
      v$.value.files.$touch();
      vWarning$.value.files.$touch();
      vWarning$.value.hasDocumentation.$touch();
    };

    const submit = () => {
      validateRequiredRules().then(validated => {
        if(validated) {
          emit("next", files);
        }
      });
    };

    /**
     *
     * @param {string} field
     */
    const fieldHasError = (field) => hasError(state, field);

    /**
     *
     * @param {string} field
     */
    const fieldHasWarning = (field) => hasWarning(state, field);

    return {
      addDescriptionAccordionId,
      addFiles,
      files,
      editIcon,
      getErrorText,
      getFunctionalState,
      getWarningText,
      isLoaded,
      isLoading,
      publishFileAccordionId,
      removeFile,
      state,
      fieldHasError,
      fieldHasWarning,
      submit,
      touch,
      v$,
      vWarning$,
    };
  },
});
</script>
