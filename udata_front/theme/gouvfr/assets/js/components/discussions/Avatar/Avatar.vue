<template>
  <div class="avatar">
    <img
      :src="avatarUrl"
      :width="size"
      :height="size"
      loading="lazy"
      alt=""
    />
  </div>
</template>

<script>
import useUserAvatar from "../../../composables/useUserAvatar";

export default {
  props: {
    user: {
      /** @type {import("vue").PropType<import("../../../types").User>} */
      type: Object,
      required: true,
    },
    size: {
      type: Number,
      default: 40,
    },
  },
  setup(props) {
    const avatarUrl = useUserAvatar(props.user, props.size);
    return {
      avatarUrl,
    }
  },
};
</script>
