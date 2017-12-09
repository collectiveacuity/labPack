function (doc, oldDoc) {
    if (doc._deleted) {
        requireUser(oldDoc.user_id);
        // Skip other validation because a deletion has no other properties:
        return;
    }
    // Require user_id
    if (typeof(doc.user_id) == 'undefined' || !doc.user_id) {
        throw({forbidden: "Missing required user_id"});
    }
    if (oldDoc == null) {
        // The user_id property must match the user creating the document:
        requireUser(doc.user_id)
    } else {
        // Only users with the existing doc's user_id can edit the doc
        requireUser(oldDoc.user_id);
        // The user_id property is immutable:
        if (doc.user_id != oldDoc.user_id) {
            throw({forbidden: "Can't change user_id"});
        }
    }
    // Finally, assign the document to the read channels in the list:
    channel(doc.user_id); 
}