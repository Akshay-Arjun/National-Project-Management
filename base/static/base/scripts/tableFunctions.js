function sortTable(tableId, col, type) {
  let table = document.getElementById(tableId);
  let rows = table.rows;

  let sort_count = 0;
  let sorting =true;

  while (sorting) {
    sorting = false;

    for (let i = 1; i < rows.length-1; i++) {
      let swap = false;
      let x = rows[i].querySelectorAll("th, td")[col]
      let y = rows[i + 1].querySelectorAll("th, td")[col]

      if (x.dataset.sortValue) {
        x = x.dataset.sortValue
        y = y.dataset.sortValue
      } else {
        x = x.innerHTML;
        y = y.innerHTML;
      }

      if (type === "number") {
        x = Number(x);
        y = Number(y);
      }

      if (x > y) {
        swap = true;
      }

      if (swap) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        sorting = true;
        sort_count++;
      }
    }
  }
}

function reverseTable(tableId) {
  table = document.getElementById(tableId);
  rows = table.rows;
  last_row = rows.length - 1;

  for (let i = 1; i < rows.length; i++) {
    rows[i].parentNode.insertBefore(rows[last_row], rows[i]);
  }
}


const sortHeaders = document.getElementsByClassName("sortHeader");

Array.from(sortHeaders).forEach(header => {
  header.addEventListener('click', (event) => {
      const target = event.target;
      const sorted = (target.dataset.sorted === 'true');
      if (sorted) {
        reverseTable(target.dataset.tableId);
        let arrow = target.getElementsByTagName("span")[0];
        if (arrow.innerHTML === "↑") {
          arrow.innerHTML = "↓";
        } else {
          arrow.innerHTML = "↑";
        }
      } else {
        const tableId = target.dataset.tableId;
        const tableHeaders = document.getElementById(tableId).getElementsByClassName("sortHeader")
        Array.from(tableHeaders).forEach( header2 => {
          let arrow = header2.getElementsByTagName("span")[0];
          if (arrow) {
            if (header2.dataset.sorted === 'true') {
              arrow.innerHTML = "•"
            } else {
              arrow.innerHTML = ""
            }
          } else {
            header2.innerHTML += "<span></span>";
          }

          header2.dataset.sorted = false;
        })
        sortTable(tableId, target.dataset.col, target.dataset.type);
        target.dataset.sorted = true;
        target.getElementsByTagName("span")[0].innerHTML = "↑"
      }
  })
})


function searchTable(tableId, value) {
  const filter = value.toLowerCase();
  const table = document.getElementById(tableId);
  const rows = table.getElementsByTagName("tr");

  for (i = 1; i < rows.length; i++) {
    const row = rows[i];
    let cols = Array.from(row.getElementsByTagName("td"));
    cols = cols.concat(Array.from(row.getElementsByTagName("th")));

    let shouldHide = true;

    cols.forEach(col => {
      const text = col.innerText;
      if (text.toLowerCase().indexOf(filter) > -1) {
        shouldHide = false;
      }
    });

    if (shouldHide) {
      row.style.display = "none";
    } else {
      row.style.display = "";
    }

  }
}

const searchInputs = document.getElementsByClassName("searchInput");

Array.from(searchInputs).forEach(input => {
  input.addEventListener('input', (event) => {
    const target = event.target;
    const targetTableId = target.dataset.tableId;
    const value = target.value;
    searchTable(targetTableId, value);
  });
});
