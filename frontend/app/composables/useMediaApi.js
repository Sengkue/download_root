export const useMediaApi = () => {
  // Base URL for all API requests
  const apiBaseUrl = 'http://localhost:3005/api';

  /**
   * Creates a Server-Sent Events (SSE) connection for tracking generation progress
   * @param {string} jobId - The unique job identifier
   * @returns {EventSource}
   */
  const createProgressStream = (jobId) => {
    return new EventSource(`${apiBaseUrl}/progress?jobId=${jobId}`);
  };

  /**
   * Sends a request to the Video Mixer backend
   * @param {FormData} formData - The payload containing videos, audio, and settings
   * @returns {Promise<Blob>} The generated video as a Blob
   */
  const mixVideoMontage = async (formData) => {
    const response = await fetch(`${apiBaseUrl}/video-mixer`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`Server returned ${response.status} ${response.statusText}`);
    }

    const blob = await response.blob();
    const videoPath = response.headers.get('x-video-path');
    return { blob, videoPath };
  };

  /**
   * Sends a request to the Image Slideshow backend
   * @param {FormData} formData - The payload containing images, audio, and settings
   * @returns {Promise<Blob>} The generated video as a Blob
   */
  const mixImageMontage = async (formData) => {
    const response = await fetch(`${apiBaseUrl}/editor/merge`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`Server returned ${response.status} ${response.statusText}`);
    }

    const blob = await response.blob();
    const videoPath = response.headers.get('x-video-path');
    return { blob, videoPath };
  };

  return {
    createProgressStream,
    mixVideoMontage,
    mixImageMontage
  };
};
