import React, { useEffect, useState } from 'react'

interface Submission {
  id: string
  name: string
  age: number
  gender: string
  country: string
  primary_emotion: string
}

export function SubmissionsList() {
  const [items, setItems] = useState<Submission[]>([])

  useEffect(() => {
    fetch('/api/v1/admin/submissions')
      .then((res) => res.json())
      .then((data) => setItems(data))
      .catch((err) => console.error(err))
  }, [])

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Age</th>
          <th>Country</th>
          <th>Emotion</th>
        </tr>
      </thead>
      <tbody>
        {items.map((s) => (
          <tr key={s.id}>
            <td>{s.id}</td>
            <td>{s.name}</td>
            <td>{s.age}</td>
            <td>{s.country}</td>
            <td>{s.primary_emotion}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
