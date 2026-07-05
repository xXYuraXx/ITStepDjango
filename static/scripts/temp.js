document.getElementById("input_search_by_id").addEventListener("submit", (event) => {
    event.preventDefault();
    
    var id = getElementById("input_search_by_id").value;
    window.location.href = `\{$ url "test_detail" {id} \}`
    
})
