(function () {

    var selectedSeatId; // id of selected seat

    // Handles click event on available seats
    function handleClick (event) {
        var currentSeat = document.getElementById(event.target.id);
            if (selectedSeatId) {
                /**
                * If an existing seat was selected then do the following
                * 1. un-select the previous seat
                * 2. select the new seat
                */
                var prevSeat = document.getElementById(selectedSeatId);
                prevSeat.classList.remove("selected");
                prevSeat.classList.add("available");
                currentSeat.classList.remove("available");
                currentSeat.classList.add("selected");
                selectedSeatId = event.target.id;
            } else {
                currentSeat.classList.remove("available");
                currentSeat.classList.add("selected");
                selectedSeatId = event.target.id;
            }
            document.getElementById("seatId").value = selectedSeatId;
    }

    function validateTicketForm (event) {
        // If not seat is select, prevent submit
        if (!selectedSeatId) {
            alert("Please select a seat");
            event.preventDefault();
        }
    }

    // Add event listener for available seats
    document.querySelectorAll(".available").forEach(function(node) {
        node.addEventListener("click", handleClick);
    });

    document.getElementById("ticketForm").addEventListener("submit", validateTicketForm);
})();