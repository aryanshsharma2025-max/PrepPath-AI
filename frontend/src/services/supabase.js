import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY || '';

if (!supabaseUrl || !supabasePublishableKey) {
  console.warn(
    'Supabase environment variables (VITE_SUPABASE_URL, VITE_SUPABASE_PUBLISHABLE_KEY) are missing or not set.'
  );
}

/**
 * Reusable Supabase client instance for frontend operations.
 * Uses publishable (anon) key and respects Row Level Security (RLS).
 * SUPABASE_SECRET_KEY must NEVER be used or exposed in the frontend.
 */
export const supabase = createClient(supabaseUrl, supabasePublishableKey);
