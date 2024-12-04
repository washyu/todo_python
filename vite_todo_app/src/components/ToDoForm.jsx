import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';

const ToDoForm = ({ addTodo }) => {
  const [todo, setTodo] = useState({ title: '', description: '', completed: false });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTodo({ ...todo, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addTodo(todo);
    setTodo({ title: '', description: '', completed: false });
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 2 }}>
      <TextField name="title" value={todo.title} onChange={handleChange} label="Title" required fullWidth sx={{ mb: 2 }} />
      <TextField name="description" value={todo.description} onChange={handleChange} label="Description" fullWidth sx={{ mb: 2 }} />
      <Button type="submit" variant="contained" color="primary">Add ToDo</Button>
    </Box>
  );
};

export default ToDoForm;