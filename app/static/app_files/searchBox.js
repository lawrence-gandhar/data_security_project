function searchBox(elem) {
	if ($("#searchBox").val() != "") {
		window.location = elem + $("#searchBox").val();
	}
}
