class TableUtility {

    constructor(tableId, searchId = null, searchCol = null) {
        this.table = document.getElementById(tableId);
        this.searchInput = searchId ? document.getElementById(searchId) : null;
        this.searchCol = searchCol !== null ? parseInt(searchCol) : null;

        this.sortDirection = {};

        if (this.searchInput) {
            this.enableSearch();
        }

        this.enableSorting();
    }
    enableSearch() {
        this.searchInput.addEventListener("keyup", () => {
            const filter = this.searchInput.value.toLowerCase();
            const rows = this.table.querySelectorAll("tbody tr");

            rows.forEach(row => {
                let text;
                if (this.searchCol !== null) {
                    text = row.querySelectorAll("td")[this.searchCol].innerText.toLowerCase();
                } 
                else {
                    text = row.innerText.toLowerCase();
                }

                row.style.display = text.includes(filter) ? "" : "none";
            });
        });
    }
    enableSorting() {
        const headers = this.table.querySelectorAll("thead th");

        headers.forEach((header, index) => {
            header.style.cursor = "pointer";
            header.addEventListener("click", () => this.sortColumn(index));
        });
    }

    sortColumn(colIndex) {
        const rows = Array.from(this.table.querySelectorAll("tbody tr"));
        const direction = this.sortDirection[colIndex] === "asc" ? "desc" : "asc";
        this.sortDirection[colIndex] = direction;

        rows.sort((a, b) => {
            let x = a.querySelectorAll("td")[colIndex].innerText.toLowerCase();
            let y = b.querySelectorAll("td")[colIndex].innerText.toLowerCase();

            if (direction === "asc") return x.localeCompare(y);
            return y.localeCompare(x);
        });

        const tbody = this.table.querySelector("tbody");
        rows.forEach(row => tbody.appendChild(row));
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-table]").forEach(wrapper => {
        const tableId = wrapper.getAttribute("data-table");
        const searchId = wrapper.getAttribute("data-search");
        const searchCol = wrapper.getAttribute("data-search-col");

        new TableUtility(tableId, searchId, searchCol);
    });
});
