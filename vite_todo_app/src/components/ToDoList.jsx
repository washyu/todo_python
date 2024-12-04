import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ToDoItem from './ToDoItem';
import ToDoForm from './ToDoForm';
import { Container, Typography, List } from '@mui/material';

const ToDoList = () => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    const response = await axios.get('http://127.0.0.1:8000/api/todos');
    setTodos(response.data);
  };

  const addTodo = async (todo) => {
    const response = await axios.post('http://127.0.0.1:8000/api/todos', todo);
    setTodos([...todos, response.data]);
  };

  const updateTodo = async (id, updatedTodo) => {
    const response = await axios.put(`http://127.0.0.1:8000/api/todos/${id}`, updatedTodo);
    setTodos(todos.map(todo => (todo.id === id ? response.data : todo)));
  };

  const deleteTodo = async (id) => {
    await axios.delete(`http://127.0.0.1:8000/api/todos/${id}`);
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        ToDo List
      </Typography>
      <ToDoForm addTodo={addTodo} />
      <List>
        {todos.map(todo => (
          <ToDoItem key={todo.id} todo={todo} updateTodo={updateTodo} deleteTodo={deleteTodo} />
        ))}
      </List>
    </Container>
  );
};

export default ToDoList;