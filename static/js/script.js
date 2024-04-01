document.addEventListener("DOMContentLoaded", function() {
    const detailsElement = document.getElementById('event-details');
    const moreDetailsButton = document.getElementById('more-details-btn');

    // Function to display event details in the sidebar based on the clicked row
    function showEventDetailsInSidebar(clickedRow) {
        // Extracting text content directly from the clicked row's cells
        const eventDetails = {
            date: clickedRow.cells[0].textContent,
            startET: clickedRow.cells[1].textContent || 'TBD',
            visitorTeam: clickedRow.cells[2].textContent,
            homeTeam: clickedRow.cells[3].textContent,
            location: clickedRow.cells[4].textContent,
            arena: clickedRow.cells[5].textContent,
        };

        // New lines to set data-city and data-team attributes on the More Details button
        const city = clickedRow.getAttribute('data-city');
        const team = clickedRow.getAttribute('data-team');
        moreDetailsButton.setAttribute('data-city', city);
        moreDetailsButton.setAttribute('data-team', team);

        // Building the details HTML to display
        const detailsHtml = `
            <strong>Date:</strong> ${eventDetails.date}<br>
            <strong>Start (ET):</strong> ${eventDetails.startET}<br>
            <strong>Visitor Team:</strong> ${eventDetails.visitorTeam}<br>
            <strong>Home Team:</strong> ${eventDetails.homeTeam}<br>
            <strong>Location:</strong> ${eventDetails.location}<br>
            <strong>Arena:</strong> ${eventDetails.arena}
        `;

        // Updating the sidebar with the event details
        detailsElement.innerHTML = detailsHtml;
        moreDetailsButton.style.display = 'block'; // Show the "More Details" button

        // Setting the data-event-id attribute for the "More Details" button
        const eventId = clickedRow.dataset.eventId;
        moreDetailsButton.setAttribute('data-event-id', eventId);

        // Highlight the clicked row and clear previous highlights
        document.querySelectorAll('tbody tr').forEach(row => {
            row.classList.remove('highlighted'); // Remove highlight from all rows
        });
        clickedRow.classList.add('highlighted'); // Add highlight to the clicked row
    }

    // Attaching click event listeners to table rows
    document.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', function() {
            showEventDetailsInSidebar(this); // Pass the clicked row itself
        });
    });

    // Optional: Redirect to the event details page when the "More Details" button is clicked
    moreDetailsButton.addEventListener('click', function() {
        const eventId = this.getAttribute('data-event-id');
        const city = this.getAttribute('data-city'); // Ensure these are being set
        const team = this.getAttribute('data-team');
        if(city && team && eventId) { // Check if values are not null
            window.location.href = `/event-details/${city}/${team}/${eventId}`;
        } else {
            console.error('Missing data for event details URL');
            // Optionally, handle this error with user feedback
        }
    });
});
