<script setup lang="ts">
import { onMounted, ref } from "vue";
import type { Contact, ContactIn } from "../contacts";
import ContactForm from "../components/ContactForm.vue";

const contacts = ref<Contact[]>([]);

onMounted(async () => {
  const response = await fetch("http://127.0.0.1:8000/api/contacts");
  const res_json = await response.json();
  contacts.value = res_json;
});

const contactForm = ref<typeof ContactForm>();

const addContact = async (contact: ContactIn) => {
  const response = await fetch("http://127.0.0.1:8000/api/contacts", {
    method: "POST",
    body: JSON.stringify(contact)
  });
  const res_json = await response.json();
  if (response.ok) {
    contacts.value.push(res_json);
    contactForm.value?.clear();
  }
  console.log(res_json);
};
</script>

<template>
  <table>
    <tbody>
      <tr v-for="contact in contacts" :key="contact.id">
        <td>{{ contact.name }}</td>
        <td>{{ contact.phone_number }}</td>
        <td>{{ contact.email }}</td>
        <td>
          <router-link :to="{ name: 'contact-detail', params: { id: contact.id } }"
            >Detail</router-link
          >
        </td>
      </tr>
    </tbody>
  </table>
  <ContactForm button-text="Add Contact" @submitted="addContact" ref="contactForm" />
</template>
