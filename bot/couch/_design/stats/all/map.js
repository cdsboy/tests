function(doc) {
  if (doc.type == "stat") {
    emit(doc.username, doc);
  }
}
