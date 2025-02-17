import RemoveMarkdown from "remove-markdown";
import markdown from "./markdown";
import dayjs from "dayjs/esm";
import { useI18n } from 'vue-i18n';
import { readonly } from "vue";

export const truncate = (val, length = 300) => {
  if (typeof val !== "string") return;
  return val.length > length ? val.slice(0, length) + "…" : val; //TODO, maybe® : properly truncate words
};

export const excerpt = (val, length = 300) => {
  if (typeof val !== "string") return;
  return truncate(RemoveMarkdown(val), length);
};

export const filesize = (val) => {
    const { t } = useI18n();
    const suffix = t('B')
    const units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    for (let unit of units) {
        if (Math.abs(val) < 1024.0) {
          return `${val.toFixed(1)}${unit}${suffix}`
        }
        val /= 1024.0
    }
    return `${val.toFixed(1)}Y${suffix}`
}

/**
 * Format date based on locale.
 * @param {Date | string} date
 * @returns {string}
 */
export const formatDate = (date, format = 'LL') => {
  return dayjs(date).format(format);
}

/**
 * Format date as relative from now.
 * It displays "today" or dayjs.fromNow content, based on date.
 * @param {Date | string} date
 * @returns {string}
 */
export const formatFromNow = (date) => {
  const { t } = useI18n();
  const today = dayjs().startOf("date");
  const dateWithoutTime = dayjs(date).startOf("date");
  if(today.isSame(dateWithoutTime)) {
    return t("today");
  }
  return dayjs(date).fromNow();
}

/**
 * Format date relative form now if date is less than a month ago.
 * Otherwise, show a formatted date.
 * @param {Date | string} date
 * @returns {string}
 */
export const formatRelativeIfRecentDate = (date) => {
  const { t } = useI18n();
  const today = dayjs().startOf("date");
  const dateWithoutTime = dayjs(date).startOf("date");
  const DONT_ROUND_DIFF = true;
  if(today.diff(dateWithoutTime, 'month', DONT_ROUND_DIFF) > 1) {
    return t("on {date}", {date: formatDate(date)});
  }
  return formatFromNow(date);
}

export const CLOSED_FORMATS = readonly(/** @type {const} */(['pdf', 'doc', 'docx', 'word', 'xls', 'excel', 'xlsx']));

export const RESOURCE_TYPE = readonly(/** @type {const} */(["main", "documentation", "update", "api", "code", "other"]));

/**
 *
 * @param {import("./types").ResourceType} type
 */
export const getResourceLabel = (type) => {
  const { t } = useI18n();
  switch(type) {
    case "main":
      return t("Main file");
    case "documentation":
      return t("Documentation");
    case "update":
      return t("Update");
    case "api":
      return t("API");
    case "code":
      return t("Source code");
    case "other":
      return t("Other");
  }
}
/**
 * Checks if a value is in an array
 * @template U
 * @template {U} T
 * @param {ReadonlyArray<T>} array
 * @param {U} value
 * @returns {value is T}
 */
const includeInSubtype = (array, value) => {
  return array.includes(/** @type {T} **/(value));
};

/**
 *
 * @param {string } format
 */
export const isClosedFormat = (format) => includeInSubtype(CLOSED_FORMATS, format);
export const UUIDRegExp = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;

export const resourceUrlRegExp = new RegExp(
  "resources\/(" +
  UUIDRegExp.source +
  ")?$", UUIDRegExp.flags);

export const previousResourceUrlRegExp = new RegExp(
  "resource-(" +
  UUIDRegExp.source +
  ")?$", UUIDRegExp.flags);

export { markdown };
