function(doc) {
  if (doc.type == "stat") {
    emit(doc.lines, doc);
  }
}
