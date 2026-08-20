import { supabase } from './supabase';

/**
 * Sign up a new user with Email and Password
 * @param {string} email 
 * @param {string} password 
 * @param {object} [data] - Optional metadata (e.g. full_name)
 */
export async function signUp(email, password, data = {}) {
  const { data: authData, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data,
    },
  });

  if (error) {
    throw error;
  }

  return authData;
}

/**
 * Sign in an existing user with Email and Password
 * @param {string} email 
 * @param {string} password 
 */
export async function signIn(email, password) {
  const { data: authData, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    throw error;
  }

  return authData;
}

/**
 * Sign out the current user session
 */
export async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) {
    throw error;
  }
}

/**
 * Get the currently authenticated user from active session
 */
export async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) {
    console.error('Error fetching current user:', error);
    return null;
  }
  return user;
}

/**
 * Get the current active session
 */
export async function getSession() {
  const { data: { session }, error } = await supabase.auth.getSession();
  if (error) {
    console.error('Error fetching current session:', error);
    return null;
  }
  return session;
}
