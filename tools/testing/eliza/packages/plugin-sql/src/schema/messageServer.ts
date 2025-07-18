import { pgTable, text, jsonb, timestamp } from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';

export const messageServerTable = pgTable('message_servers', {
  id: text('id').primaryKey(), // UUID stored as text
  name: text('name').notNull(),
  sourceType: text('source_type').notNull(),
  sourceId: text('source_id'),
  metadata: jsonb('metadata'),
  createdAt: timestamp('created_at', { mode: 'date' })
    .default(sql`CURRENT_TIMESTAMP`)
    .notNull(),
  updatedAt: timestamp('updated_at', { mode: 'date' })
    .default(sql`CURRENT_TIMESTAMP`)
    .notNull(),
});
