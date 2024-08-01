import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ name: '', category: '', details: '' });
  const [analysis, setAnalysis] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5000/api/tasks')
      .then(response => setTasks(response.data))
      .catch(error => console.error('Error fetching tasks:', error));
  }, []);

  const handleAddTask = () => {
    axios.post('http://localhost:5000/api/tasks', newTask)
      .then(response => {
        setTasks([...tasks, response.data]);
        setNewTask({ name: '', category: '', details: '' });
      })
      .catch(error => console.error('Error adding task:', error));
  };

  const handleAnalyzeTask = () => {
    axios.post('http://localhost:5000/api/tasks/analyze', { name: newTask.name })
      .then(response => setAnalysis(response.data.analysis))
      .catch(error => console.error('Error analyzing task:', error));
  };

  return (
    <div>
      <h1>Task Manager</h1>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.name} - {task.category} - {task.details} - {task.analysis}</li>
        ))}
      </ul>
      <input 
        type="text" 
        value={newTask.name} 
        onChange={e => setNewTask({ ...newTask, name: e.target.value })} 
        placeholder="Task name"
      />
      <input 
        type="text" 
        value={newTask.category} 
        onChange={e => setNewTask({ ...newTask, category: e.target.value })} 
        placeholder="Category"
      />
      <input 
        type="text" 
        value={newTask.details} 
        onChange={e => setNewTask({ ...newTask, details: e.target.value })} 
        placeholder="Details"
      />
      <button onClick={handleAddTask}>Add Task</button>
      <button onClick={handleAnalyzeTask}>Analyze Task</button>
      {analysis && <p>Analysis: {analysis}</p>}
    </div>
  );
}

export default App;
