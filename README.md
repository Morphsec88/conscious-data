# Conscious Data

The core idea of the model is that when data is saved, the system writes the 
storage’s unique identifier into the file’s metadata. This identifier may be a 
simple name, or—when needed—an additional structural element such as a layer or row. 
The metadata is not visible to the user, but the directory system can read it 
directly, eliminating the need for searching or indexing: the data becomes 
instantly accessible.

This approach can be applied to any storage type that provides a unique 
identifier; additional structural elements of the storage can also be recorded 
in the metadata when required.

The goal is a workflow where the location of the data is not determined through 
searching or inference, but can be read directly from the metadata itself. 
This results in a simpler, faster, and lower‑overhead system.

