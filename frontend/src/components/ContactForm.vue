<script setup lang="ts">
import { ref, watchEffect } from "vue";
import type { Contact, ContactIn } from "../contacts";

const props = defineProps<{
  buttonText: string;
  contact?: Contact;
}>();

const emit = defineEmits<{
  submitted: [contact: ContactIn];
}>();

const name = ref("");
const phoneNumber = ref("");
const email = ref("");

watchEffect(() => {
  name.value = props.contact?.name || "";
  phoneNumber.value = props.contact?.phone_number || "";
  email.value = props.contact?.email || "";
});

const clear = () => {
  name.value = "";
  phoneNumber.value = "";
  email.value = "";
};

defineExpose({
  clear
});
</script>
<template>
  <form @submit.prevent="emit('submitted', { name, phone_number: phoneNumber, email })">
    <table>
      <tbody>
        <tr>
          <td><label for="name">Name</label></td>
          <td><input type="text" v-model="name" id="name" required /></td>
        </tr>
        <tr>
          <td><label for="phone-number">Phone number</label></td>
          <td><input type="text" v-model="phoneNumber" id="phone-number" /></td>
        </tr>
        <tr>
          <td><label for="email">Email</label></td>
          <td><input type="email" v-model="email" id="email" /></td>
        </tr>
        <tr>
          <td>
            <button type="submit">{{ props.buttonText }}</button>
          </td>
        </tr>
      </tbody>
    </table>
  </form>
</template>
