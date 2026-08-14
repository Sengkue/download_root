import { ref, onBeforeUnmount } from 'vue';

/**
 * Composable for managing image file uploads with drag-and-drop support.
 * Handles file validation, preview URL creation, and automatic cleanup.
 */
export function useImageUpload() {
  const imageFiles = ref([]);
  const imagePreviewUrls = ref([]);
  const isDraggingImage = ref(false);

  /**
   * Revoke all current object URLs to prevent memory leaks.
   */
  const revokeUrls = () => {
    imagePreviewUrls.value.forEach((url) => URL.revokeObjectURL(url));
  };

  /**
   * Set image files and create preview object URLs.
   * Revokes any previously created URLs before setting new ones.
   * @param {File[]} files - Array of image File objects
   */
  const setImages = (files) => {
    revokeUrls();
    imageFiles.value = files;
    imagePreviewUrls.value = files.map((f) => URL.createObjectURL(f));
  };

  /**
   * Handle image files dropped onto the drop zone.
   * Filters to only accept files with image/* MIME type.
   * @param {DragEvent} event
   */
  const onDropImage = (event) => {
    isDraggingImage.value = false;
    const files = Array.from(event.dataTransfer?.files || []);
    const validFiles = files.filter((f) => f.type.startsWith('image/'));
    if (validFiles.length > 0) {
      setImages(validFiles);
    }
  };

  /**
   * Handle image files selected via the file input dialog.
   * Resets the input value so the same files can be re-selected if needed.
   * @param {Event} event
   */
  const onSelectImage = (event) => {
    const files = Array.from(event.target.files || []);
    if (files.length > 0) {
      setImages(files);
    }
    event.target.value = '';
  };

  /**
   * Reset all image state and release object URLs.
   */
  const resetImages = () => {
    revokeUrls();
    imageFiles.value = [];
    imagePreviewUrls.value = [];
  };

  // Automatically clean up object URLs when the component unmounts
  onBeforeUnmount(() => {
    revokeUrls();
  });

  return {
    imageFiles,
    imagePreviewUrls,
    isDraggingImage,
    onDropImage,
    onSelectImage,
    resetImages,
  };
}
