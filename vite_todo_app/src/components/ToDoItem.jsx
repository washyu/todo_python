import React, { useState } from 'react';
import { ListItem, ListItemText, IconButton, TextField, Button } from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';

const ToDoItem = ({ todo, updateTodo, deleteTodo }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [updatedTodo, setUpdatedTodo] = useState(todo);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUpdatedTodo({ ...updatedTodo, [name]: value });
  };

  const handleUpdate = () => {
    updateTodo(todo.id, updatedTodo);
    setIsEditing(false);
  };

  return (
    <ListItem>
      {isEditing ? (
        <div>
          <TextField name="title" value={updatedTodo.title} onChange={handleChange} label="Title" />
          <TextField name="description" value={updatedTodo.description} onChange={handleChange} label="Description" />
          <Button onClick={handleUpdate} variant="contained" color="primary">Update</Button>
        </div>
      ) : (
        <ListItemText primary={todo.title} secondary={todo.description} />
      )}
      <IconButton onClick={() => setIsEditing(true)} color="primary">
        <Edit />
      </IconButton>
      <IconButton onClick={() => deleteTodo(todo.id)} color="secondary">
        <Delete />
      </IconButton>
    </ListItem>
  );
};

export default ToDoItem;