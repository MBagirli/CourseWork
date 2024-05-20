const pageState = {
    pageNumber: 1,
    perPage: 5
};

let searchState = {
    pageNumber: 1,
    perPage: 5
};

let searchMode = false;

const spinner = document.querySelector(".spinner");
const contents = document.getElementById("contents");
const prevBtn = document.getElementById("previous_btn");
const nextBtn = document.getElementById("next_btn");
const submitBtn = document.getElementById("submit");
const carModelInput = document.getElementById("carModel");
const driverNameInput = document.getElementById("driverName");
const regionInput = document.getElementById("region");
const ratingInput = document.getElementById("rating");
const deleteBtns = document.getElementsByClassName('delete_btns');
const searchBtn = document.getElementById("searchBtn");

document.addEventListener("DOMContentLoaded", () => {
    getData(pageState.pageNumber, pageState.perPage);
});

document.getElementById('openPopup').addEventListener('click', () => {
    document.getElementById('popupContainer').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('popupContainer').style.display = 'none';
});

submitBtn.addEventListener('click', () => {
    const carData = {
        car_model: carModelInput.value,
        driver_name: driverNameInput.value,
        country_region: regionInput.value,
        rating: ratingInput.value
    };
    addCarInfo(carData);
});

nextBtn.addEventListener('click', () => {
    if (!searchMode) {
        pageState.pageNumber += 1;
        getData(pageState.pageNumber, pageState.perPage);
    } else {
        searchState.pageNumber += 1;
        search();
    }
});

prevBtn.addEventListener('click', () => {
    if (!searchMode) {
        pageState.pageNumber -= 1;
        getData(pageState.pageNumber, pageState.perPage);
    } else {
        searchState.pageNumber -= 1;
        search();
    }
});

searchBtn.addEventListener('click', () => {
    search();
});

function getData(page, perPage) {
    contents.innerHTML = `
      <li>
        <span>Car model</span>
        <span>Driver's name</span>
        <span>Region</span>
        <span>Rating</span>
        <span><button id="invisible_btn">X</button></span>
      </li>
     `;
    spinner.style.display = 'block';
    fetch(`https://coursework-6sjx.onrender.com/cars?page=${page}&per_page=${perPage}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            spinner.style.display = 'none';
            contents.innerHTML = '';
            data.cars.forEach(car => {
                contents.innerHTML += `
                    <li>
                        <span>${car.car_model}</span>
                        <span>${car.driver_name}</span>
                        <span>${car.country_region}</span>
                        <span>${car.rating}</span>
                        <span><button class="delete_btns" id="${car.id}">X</button></span>
                    </li>
                `;
            });
            nextBtn.style.display = data.has_next ? 'block' : 'none';
            prevBtn.style.display = data.has_prev ? 'block' : 'none';
            addDeleteButtonListeners();
        })
        .catch(error => {
            contents.innerHTML = `${error}`;
        });
}

function addCarInfo(data) {
    fetch('https://coursework-6sjx.onrender.com/add_car_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(() => {
            alert("Something went wrong!");
        });
}

function search() {
    const keyword = document.getElementById('searchInput').value.trim();
    if (keyword) {
        searchMode = true;
        pageState.pageNumber=1;
    } else {
        searchMode = false;
        searchState.pageNumber=1;
    }
    contents.innerHTML = `
      <li>
        <span>Car model</span>
        <span>Driver's name</span>
        <span>Region</span>
        <span>Rating</span>
        <span><button id="invisible_btn">X</button></span>
      </li>
     `;
    spinner.style.display = 'block';

    fetch(`https://coursework-6sjx.onrender.com/search?keyword=${keyword}&page=${searchState.pageNumber}&per_page=${searchState.perPage}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to search');
            }
            return response.json();
        })
        .then(data => {
            spinner.style.display = 'none';
            contents.innerHTML = '';
            data.cars.forEach(car => {
                contents.innerHTML += `
                    <li>
                        <span>${car.car_model}</span>
                        <span>${car.driver_name}</span>
                        <span>${car.country_region}</span>
                        <span>${car.rating}</span>
                        <span><button class="delete_btns" id="${car.id}">X</button></span>
                    </li>
                `;
            });
            nextBtn.style.display = data.has_next ? 'block' : 'none';
            prevBtn.style.display = data.has_prev ? 'block' : 'none';
            addDeleteButtonListeners();
        })
        .catch(error => {
            console.error(error);
        });
}

function addDeleteButtonListeners() {
    for (let i = 0; i < deleteBtns.length; i++) {
        deleteBtns[i].addEventListener('click', function() {
            const id = this.id;
            fetch(`/delete_element/${id}`, {
                    method: 'DELETE'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to delete element');
                    }
                    return response.json();
                })
                .then(data => {
                    alert(data.message + " Reload the page!");
                })
                .catch(error => {
                    alert("Something went wrong!");
                });
        });
    }
}
