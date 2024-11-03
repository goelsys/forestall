<script>
  const toggleButton = document.querySelector('.toggle-button');
  const cardBody = document.querySelector('.card-body');
  const cardFooter = document.querySelector('.card-footer');

  toggleButton.addEventListener('click', () => {
    cardBody.classList.toggle('hidden');
    cardFooter.classList.toggle('hidden');
    // Optionally, toggle the button text:
    toggleButton.textContent = toggleButton.textContent === 'Hide' ? 'Show' : 'Hide';
  });
</script>