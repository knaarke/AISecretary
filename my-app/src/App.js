import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');

  useEffect(() => {
    axios.get('/api/tasks')
      .then(response => {
        setTasks(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the tasks!', error);
      });
  }, []);

  const addTask = () => {
    const newTask = { id: tasks.length + 1, title };
    axios.post('/api/tasks', newTask)
      .then(response => {
        setTasks([...tasks, response.data]);
        setTitle('');
      })
      .catch(error => {
        console.error('There was an error adding the task!', error);
      });
  };

  return (
    <div className="App">
      <h1>Task List</h1>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.title}</li>
        ))}
      </ul>
      <input
        type="text"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <button onClick={addTask}>Add Task</button>
    </div>
  );
}

export default App;
