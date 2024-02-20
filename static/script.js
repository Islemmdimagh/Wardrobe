document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch one random item from each category
    async function getRandomItems() {
        const categories = document.querySelectorAll('.category');
        const randomItems = [];

        // Loop through each category
        categories.forEach(category => {
            const images = category.querySelectorAll('.image-wrapper img');
            if (images.length > 0) {
                const randomIndex = Math.floor(Math.random() * images.length);
                randomItems.push(images[randomIndex].src);
            }
        });

        return randomItems;
    }

    // Function to display the outfit in a popup
    function displayOutfit(outfit) {
        // Create popup container
        const popupContainer = document.createElement('div');
        popupContainer.classList.add('outfit-popup-container');

        // Create popup content
        const popupContent = document.createElement('div');
        popupContent.classList.add('outfit-popup');
        outfit.forEach(item => {
            const image = document.createElement('img');
            image.src = item;
            popupContent.appendChild(image);
        });

        // Create close button
        const closeButton = document.createElement('button');
        closeButton.textContent = 'Close';
        closeButton.addEventListener('click', () => {
            popupContainer.remove(); // Remove the popup when close button is clicked
        });

        // Add popup content and close button to container
        popupContainer.appendChild(popupContent);
        popupContainer.appendChild(closeButton);

        // Append container to body
        document.body.appendChild(popupContainer);
    }

    // Event listener for "Create Outfit" button click
    const createOutfitBtn = document.getElementById('create-outfit-btn');
    createOutfitBtn.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent the default form submission
        const randomItems = await getRandomItems();
        if (randomItems.length > 0) {
            displayOutfit(randomItems);
        } else {
            alert('No items available in one or more categories.');
        }
    });

    // Event delegation for delete buttons
    document.addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-btn')) {
            event.preventDefault();
            const form = event.target.closest('form');
            const formData = new FormData(form);
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    form.closest('.image-wrapper').remove();
                } else {
                    console.error('Delete request failed:', response.status);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });

    // Close the popup when clicking outside of it
    document.addEventListener('click', closePopupOutside);

    function closePopupOutside(event) {
        const popupContainer = document.querySelector('.outfit-popup-container');
        if (popupContainer && !popupContainer.contains(event.target) && event.target !== createOutfitBtn) {
            popupContainer.remove();
        }
    }
});
