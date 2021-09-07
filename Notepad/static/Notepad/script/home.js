var allNotes = {
    f: ["hi", "im", "working"]
}

var clickedNotebook = null;
var clickedNotebookButton = null;

function addNotebook () {
    let ulOfNotebooks = document.getElementById("ul-of-notebooks");

    let newNotebook = prompt("لطفا نام نوتبوک را وارد کنید");
    if (newNotebook == "") {
        alert("باید حتما نامی را انتخاب کنید");
        return
    }
    else if (newNotebook == null) {
        return
    }
    for (i in allNotes) {
        if (newNotebook == i) {
            alert("نمی توانید نام تکراری انتخاب کنید.")
            return
        }
    }

    let newLi = document.createElement("li");
    let newButton = document.createElement("button");
    let newDiv = document.createElement("div");
    let newP = document.createElement("p");

    newLi.className = "list-item"

    newLi.appendChild(newButton);
    newButton.appendChild(newDiv);
    newButton.appendChild(newP)
    newButton.className = "list-button";
    newDiv.className = "delete-item";
    newP.innerHTML = newNotebook;

    newButton.onclick = function() {
        var ulOfNotes = document.getElementById("ul-of-notes");

        let btns = document.querySelectorAll("#ul-of-notebooks .list-button");
        let counter = 0;
        while (counter < btns.length) {
            btns[counter].style.background = "#4c5c68";
            btns[counter].style.color = "#fff";
            counter ++
        }
        newButton.style.background = "#c1f3f0";
        newButton.style.color = "#4c5c68";

        while (ulOfNotes.children[0]) {
            ulOfNotes.removeChild(ulOfNotes.lastChild);
        }
        
        for (i in allNotes) {
            if (i == newButton.lastChild.innerHTML) {
                clickedNotebook = i;
                clickedNotebookButton = newButton;
                for (j in allNotes[i]) {
                    let newLi = document.createElement("li");
                    let newButton = document.createElement("button");
                    let newDiv = document.createElement("div");
                    let newP = document.createElement("p");

                    newLi.appendChild(newButton);
                    newButton.appendChild(newDiv);
                    newButton.appendChild(newP);

                    newButton.className = "list-button";
                    newDiv.className = "delete-item";
                    newP.innerHTML = allNotes[i][j];

                    ulOfNotes.prepend(newLi);
                }
            }
        }
        document.getElementById("notes-id").style.transform = "translate(0)";
        document.getElementById("notes-id").style.zIndex = 1;
    }
    // let inner = `<li><button class="list-button"><div class="delete-item">x</div><p>${newNotebook}</p></button></li>`
    
    allNotes[newNotebook] = [];
    ulOfNotebooks.prepend(newLi);

}

function addNote () {
    let ulOfNotes = document.getElementById("ul-of-notes");

    let newNote = prompt("نام نوت جدید را وارد کنید");

    allNotes[clickedNotebook].push(newNote);

    let newLi = document.createElement("li");
    let newNoteCode = `<button class="list-button"><div class=-delete-item"></div><p>${newNote}</p></button>`
    newLi.className = "list-item";
    newLi.innerHTML = newNoteCode;
    ulOfNotes.prepend(newLi);
}