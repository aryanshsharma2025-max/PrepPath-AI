const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Fetch health status from FastAPI backend
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch backend health status:', error);
    return {
      status: 'offline',
      error: error.message
    };
  }
}

/**
 * Upload and analyze scholarship PDF document via backend API
 * @param {File} file - Selected PDF file
 */
export async function analyzeOpportunity(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/opportunities/analyze`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        error: data.error || `Server error (${response.status})`
      };
    }

    return data;
  } catch (error) {
    console.error('API analyzeOpportunity error:', error);
    return {
      success: false,
      error: `API Request Failed: ${error.message || error}`
    };
  }
}

export async function getProfile() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/profile`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('API getProfile error:', error);
    return null;
  }
}

export async function updateProfile(profileData) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profileData)
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('API updateProfile error:', error);
    return null;
  }
}

export async function checkEligibility(opportunityId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/opportunities/${opportunityId}/eligibility`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('API checkEligibility error:', error);
    return null;
  }
}
