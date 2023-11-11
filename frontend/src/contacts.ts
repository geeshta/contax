interface Contact {
  id: number;
  name: string;
  phone_number?: string;
  email?: string;
}

interface ContactIn {
  name: string;
  phone_number?: string;
  email?: string;
}

export type { Contact, ContactIn };
