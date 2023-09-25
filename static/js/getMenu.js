const menuJSON = '../static/assets/json/menu_items.json';
const menuEl = document.getElementById('menu');

fetch(menuJSON).then(function (response) {return response.json();}).then(function (jsonObject) {
    const menu = jsonObject.menu;
    displayDetails(menu);
});

function displayDetails(entry) {
    for (listing in entry) {
        const listingEl = document.createElement('li');
        listingEl.textContent = listing.toUpperCase();
        menuEl.append(document.createElement('br'));
        menuEl.append(listingEl);

        if (listing.toLowerCase() == "burgers") {
            let burgers = getEntries(entry[listing]);
            displayEntries(burgers);
        } else if (listing.toLowerCase() == "sandwiches") {
            let sandwiches = getEntries(entry[listing]);
            displayEntries(sandwiches);
        } else if (listing.toLowerCase() == "sides") {
            let sides = getEntries(entry[listing]);
            displayEntries(sides);
        } else if (listing.toLowerCase() == "favorites") {
            let favorites = getEntries(entry[listing]);
            displayEntries(favorites);
        } else if (listing.toLowerCase() == "dinners") {
            let dinners = getEntries(entry[listing]);
            displayEntries(dinners);
        } else if (listing.toLowerCase() == "baskets") {
            let baskets = getEntries(entry[listing]);
            displayEntries(baskets);
        } else if (listing.toLowerCase() == "lite plates") {
            let litePlates = getEntries(entry[listing]);
            displayEntries(litePlates);
        } else if (listing.toLowerCase() == "salads") {
            let salads = getEntries(entry[listing]);
            displayEntries(salads);
        } else if (listing.toLowerCase() == "dressings") {
            let dressings = getEntries(entry[listing]);
            displayEntries(dressings);
        } else if (listing.toLowerCase() == "kiddie") {
            let kiddies = getEntries(entry[listing]);
            displayEntries(kiddies);
        } else if (listing.toLowerCase() == "beverages") {
            let beverages = getEntries(entry[listing]);
            displayEntries(beverages);
        } else if (listing.toLowerCase() == "sweets") {
            let sweets = getEntries(entry[listing]);
            displayEntries(sweets);
        } else {
            continue;
        }
    }
}

function getEntries(entriesObj) {
    let entries = [];
    let entriesArr = Object.entries(entriesObj);
    entriesArr.forEach((entry) => {
        entries.push(entry)
    });
    return entries
}

function displayEntries(entriesArr) {
    const skips = [
        "sides",
        "size",
        "flavor",
        "entree",
        "beverages",
        "cookies",
        "sliced cakes",
        "loaf cakes"
    ];
    entriesArr.forEach((entry) => {
        if (!(entry[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"])) {
            if (skips.includes(entry[0])) {
                if (typeof entry[1] === 'object') {
                    for (subEntry in entry[1]) {
                        if (typeof entry[1][subEntry] === 'object') {
                            const entryListingEl = document.createElement('li');
                            for (index in entry[1][subEntry]) {
                                item = index;
                                entryListingEl.textContent = item.toLowerCase();
                                menuEl.append(entryListingEl);
                            }
                        } else {
                            const entryListingEl = document.createElement('li');
                            item = entry[1][subEntry];
                            entryListingEl.textContent = item.toLowerCase();
                            menuEl.append(entryListingEl);
                        }
                    }
                } else {
                    const entryListingEl = document.createElement('li');
                    entryListingEl.textContent = entry[0].toLowerCase();
                    menuEl.append(entryListingEl);
                }
            } else {
                const entryListingEl = document.createElement('li');
                entryListingEl.textContent = entry[0].toLowerCase();
                menuEl.append(entryListingEl);
            }
        } else {
            const entryListingEl = document.createElement('li');
            if (typeof entry[1] === 'object') {
                entryListingEl.textContent = Object.keys(entry[1])[0];
            } else {
                entryListingEl.textContent = entry[1].toLowerCase();
            }            
            menuEl.append(entryListingEl);
        }
    });
}