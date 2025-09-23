import { useState } from "react";

interface Employee {
  employee_id: string;
  name: string;
  age: number;
  department: string;
}

export default function Employees() {
  const [employees, setEmployees] = useState<Employee[]>([
    { employee_id: "1", name: "Alice", age: 28, department: "HR" },
    { employee_id: "2", name: "Bob", age: 32, department: "IT" },
  ]);

  const handleDelete = (id: string) => {
    setEmployees((prev) => prev.filter((e) => e.employee_id !== id));
  };

  const handleMove = (index: number, direction: "up" | "down") => {
    const newList = [...employees];
    const swapIndex = direction === "up" ? index - 1 : index + 1;
    if (swapIndex < 0 || swapIndex >= newList.length) return;
    [newList[index], newList[swapIndex]] = [newList[swapIndex], newList[index]];
    setEmployees(newList);
  };

  const handleUpdate = (id: string) => {
    const name = prompt("Enter new name");
    if (!name) return;
    setEmployees((prev) =>
      prev.map((e) =>
        e.employee_id === id ? { ...e, name } : e
      )
    );
  };

  const handleAdd = () => {
    const name = prompt("Enter employee name");
    const age = Number(prompt("Enter employee age"));
    const department = prompt("Enter department");
    if (!name || !age || !department) return;
    const newEmp: Employee = {
      employee_id: String(Date.now()),
      name,
      age,
      department,
    };
    setEmployees((prev) => [...prev, newEmp]);
  };

  const handleImportCSV = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    // TODO: parse CSV and send to backend
    alert(`Imported file: ${file.name}`);
  };

  return (
    <div className="bg-white shadow p-6 rounded-lg">
      <h1 className="text-2xl font-bold mb-4">Manage Employees</h1>

      <div className="flex gap-4 mb-4">
        <button
          onClick={handleAdd}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Add Employee
        </button>
        <input
          type="file"
          accept=".csv"
          onChange={handleImportCSV}
          className="border p-2 rounded"
        />
      </div>

      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">ID</th>
            <th className="border p-2">Name</th>
            <th className="border p-2">Age</th>
            <th className="border p-2">Department</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((emp, index) => (
            <tr key={emp.employee_id}>
              <td className="border p-2">{emp.employee_id}</td>
              <td className="border p-2">{emp.name}</td>
              <td className="border p-2">{emp.age}</td>
              <td className="border p-2">{emp.department}</td>
              <td className="border p-2 flex gap-2">
                <button
                  onClick={() => handleUpdate(emp.employee_id)}
                  className="px-2 py-1 bg-blue-600 text-white rounded"
                >
                  Update
                </button>
                <button
                  onClick={() => handleDelete(emp.employee_id)}
                  className="px-2 py-1 bg-red-600 text-white rounded"
                >
                  Delete
                </button>
                <button
                  onClick={() => handleMove(index, "up")}
                  className="px-2 py-1 bg-gray-500 text-white rounded"
                >
                  ↑
                </button>
                <button
                  onClick={() => handleMove(index, "down")}
                  className="px-2 py-1 bg-gray-500 text-white rounded"
                >
                  ↓
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
