<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import ContactForm from "../components/ContactForm.vue";
import type { Contact, ContactIn } from "../contacts";

const route = useRoute();
const router = useRouter();

const contact = ref<Contact>();

onMounted(async () => {
  const response = await fetch(`http://127.0.0.1:8000/api/contacts/${route.params.id}`);
  const res_json = await response.json();
  contact.value = res_json;
  document.title = contact.value?.name || "My Contacts";
});

const contactForm = ref<typeof ContactForm>();

const updateContact = async (contactIn: ContactIn) => {
  const response = await fetch(
    `http://127.0.0.1:8000/api/contacts/${route.params.id}`,
    {
      method: "PUT",
      body: JSON.stringify(contactIn)
    }
  );
  const res_json = await response.json();
  if (response.ok) {
    contact.value = res_json;
  }
  console.log(res_json);
};

const deleteContact = async () => {
  if (confirm("Are you sure you want to delete this contact?")) {
    const response = await fetch(
      `http://127.0.0.1:8000/api/contacts/${route.params.id}`,
      {
        method: "DELETE"
      }
    );

    if (response.ok) {
      router.push({ name: "contact-list" });
    }
  }
};
</script>

<template>
  <table>
    <tbody>
      <tr>
        <td>
          <strong>{{ contact?.name }}</strong>
        </td>
      </tr>
      <tr>
        <td>
          {{ contact?.phone_number }}
        </td>
      </tr>
      <tr>
        <td>
          {{ contact?.email }}
        </td>
      </tr>
    </tbody>
  </table>
  <ContactForm
    button-text="Update Contact"
    :contact="contact"
    @submitted="updateContact"
    ref="contactForm" />
  <button @click="deleteContact">Delete Contact</button>
</template>
