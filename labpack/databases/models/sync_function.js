function (doc, oldDoc) {
    if (doc._deleted) {
        requireUser(oldDoc.uid);
        // Skip other validation because a deletion has no other properties:
        return;
    }
    // Require uid
    if (typeof(doc.uid) == 'undefined' || !doc.uid) {
        throw({forbidden: "Missing required uid"});
    }
    if (oldDoc == null) {
        // The uid property must match the user creating the document:
        requireUser(doc.uid)
    } else {
        // Only users with the existing doc's uid can edit the doc
        requireUser(oldDoc.uid);
        // The uid property is immutable:
        if (doc.uid != oldDoc.uid) {
            throw({forbidden: "Can't change uid"});
        }
    }
    // Finally, assign the document to the read channels in the list:
    channel(doc.uid); 
}