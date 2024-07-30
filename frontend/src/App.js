import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5000/api/tasks')
      .then(response => setTasks(response.data))
      .catch(error => console.error('Error fetching tasks:', error));
  }, []);

  const handleAddTask = () => {
    const task = { name: newTask };
    axios.post('http://localhost:5000/api/tasks', task)
      .then(response => setTasks([...tasks, response.data]))
      .catch(error => console.error('Error adding task:', error));
    setNewTask('');
  };

  return (
    <div>
      <h1>Task Manager</h1>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.name}</li>
        ))}
      </ul>
      <input 
        type="text" 
        value={newTask} 
        onChange={e => setNewTask(e.target.value)} 
      />
      <button onClick={handleAddTask}>Add Task</button>
    </div>
  );
}

export default App;
