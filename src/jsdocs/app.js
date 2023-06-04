const service = window.location.href+"scrapper-api.py";

// Fonction pour obtenir les noms des mangas
function getMangasNames() {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `${service}?req=getMangasName`, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    console.log("...");
    xhr.send();

    if (xhr.status === 200) {
      resolve(JSON.parse(xhr.responseText));
    } else {
      reject(xhr.status);
    }
  });
}

// Fonction pour télécharger un manga
function downloadManga(mangaNumber, value1, value2) {
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `${service}?req=choice&value=${mangaNumber}&value1=${value1}&value2=${value2}`, false);
    //xhr.setRequestHeader('Content-Type', 'application/json');
    console.log("...");
    xhr.send();

    if (xhr.status === 200) {
      var response = xhr.responseText;
      resolve(response);
    } else {
      reject(xhr.status);
    }
  });
}

const SELECT = document.querySelector("select#choice");
const SUBMITBUTTON = document.querySelector("input[type=submit]");

const waitingMangasNames = getMangasNames();

waitingMangasNames.then((response) => {
  let newHtmlOptions = "<option value=''> Choose a manga </option>";
  for (let key in response) {
    newHtmlOptions += "<option value='" + key + "'>" + response[key] + "</option>";
  }
  SELECT.innerHTML = newHtmlOptions;

  SUBMITBUTTON.addEventListener("click", () => {
 
    Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'Your work has been saved',
        showConfirmButton: false,
        timer: 1500
      })    
      
      fqfq

    let mangaNumber = document.querySelector("select#choice").value;
    let value1 = document.querySelector("input#first").value;
    let value2 = document.querySelector("input#last").value;

    const waitingDownloadManga = downloadManga(mangaNumber, value1, value2);

    waitingDownloadManga.then((response) => {
      console.log(response);

     
    })
    .catch((response) => {
      console.log(response);
    });
  });
});

waitingMangasNames.catch((response) => {
  console.log(response);
});
