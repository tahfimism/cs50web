// --- counter.js ---

if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0)
}


// Declare a variable to hold our interval's ID


function count() {
    let n = parseInt(localStorage.getItem('counter'));
    let gg = document.querySelector("#gg");
    n++; // Increment the counter
    gg.innerHTML = n;

    // Check if the counter has reached 10
    
    localStorage.setItem('counter', n)
}

// Use the correct event listener: DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#gg').innerHTML = localStorage.getItem('counter');
    // Store the ID that setInterval returns
    document.querySelector('button').onclick = count


});
