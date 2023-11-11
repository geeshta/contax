<script setup lang="ts">
import { json } from "stream/consumers";
import { onMounted, ref } from "vue";
interface Contact {
  id: number;
  name: string;
  phone_number?: string;
  email?: string;
}

const contacts = ref<Contact[]>([]);

const newName = ref("");
const newPhoneNumber = ref("");
const newEmail = ref("");

const addContact = async (name: string, phoneNumber?: string, email?: string) => {
  const response = await fetch("http://127.0.0.1:8000/api/contacts", {
    method: "POST",
    body: JSON.stringify({ name, phone_number: phoneNumber, email })
  });
  const res_json = await response.json();
  if (response.ok) {
    newName.value = "";
    newPhoneNumber.value = "";
    newEmail.value = "";

    contacts.value.push(res_json);
  }
  console.log(res_json);
};

onMounted(async () => {
  const response = await fetch("http://127.0.0.1:8000/api/contacts");
  const res_json = await response.json();
  contacts.value = res_json;
});
</script>

<template>
  <table>
    <tbody>
      <tr v-for="contact in contacts" :key="contact.id">
        <td>{{ contact.name }}</td>
        <td>{{ contact.phone_number }}</td>
        <td>{{ contact.email }}</td>
      </tr>
    </tbody>
  </table>
  <form @submit.prevent="addContact(newName, newPhoneNumber, newEmail)">
    <table>
      <tbody>
        <tr>
          <td><label for="name">Name</label></td>
          <td><input type="text" v-model="newName" id="name" required /></td>
        </tr>
        <tr>
          <td><label for="phone-number">Phone number</label></td>
          <td><input type="text" v-model="newPhoneNumber" id="phone-number" /></td>
        </tr>
        <tr>
          <td><label for="email">Email</label></td>
          <td><input type="email" v-model="newEmail" id="email" /></td>
        </tr>
        <tr>
          <td><button type="submit">Add Contact</button></td>
        </tr>
      </tbody>
    </table>
  </form>
</template>
