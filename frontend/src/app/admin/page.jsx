"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, logout } from "../../lib/api";

export default function Admin() {
  const [analytics, setAnalytics] = useState(null);
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api("/auth/me/"),
      api("/admin/analytics/"),
      api("/admin/users/"),
    ])
      .then(([me, analyticsData, usersData]) => {
        if (me.role !== "admin") {
          throw new Error("Administrator access required");
        }

        setAnalytics(analyticsData);
        setUsers(usersData);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  const handleLogout = () => {
    logout();
    window.location.href = "/login";
  };

  if (error) {
    return (
      <main className="container page">
        <p className="error">{error}</p>
        <Link href="/login">Login</Link>
      </main>
    );
  }

  if (!analytics) {
    return (
      <main className="container page">
        Loading admin intelligence...
      </main>
    );
  }

  return (
    <>
      <div className="adminbar">
        CyberGuard Security Operations · Administrator
      </div>

      <nav className="nav">
        <Link className="logo" href="/">
          Cyber<span>Guard</span>
        </Link>

        <div className="links">
          <Link href="/dashboard">User Site</Link>
          <Link href="/incident">Incident Lab</Link>

          <button
            className="button red"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="container page">
        <p className="eyebrow">
          SECURITY ANALYTICS
        </p>

        <h1>
          Platform Intelligence
        </h1>

        <div className="cards">
          <div className="card">
            <div className="stat">
              {analytics.users}
            </div>
            Users
          </div>

          <div className="card">
            <div className="stat">
              {analytics.courses}
            </div>
            Courses
          </div>

          <div className="card">
            <div className="stat">
              {analytics.attempts}
            </div>
            Attempts
          </div>

          <div className="card">
            <div className="stat">
              {analytics.completed_sessions}
            </div>
            Completed Sessions
          </div>
        </div>

        <div className="grid">
          <div className="card">
            <h2>
              Common Weaknesses
            </h2>

            {analytics.weaknesses?.map((item) => (
              <div
                className="metric"
                key={item.type}
              >
                <span>
                  {item.type}
                </span>

                <strong>
                  {item.score}%
                </strong>

                <div className="progress">
                  <i
                    style={{
                      width: `${item.score}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="card">
            <h2>
              Priority Users
            </h2>

            {analytics.high_risk_users?.map((user) => (
              <p key={user.username}>
                <strong>
                  {user.username}
                </strong>{" "}
                · Level {user.profile__level} ·{" "}
                {user.profile__points} XP
              </p>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>
            Registered Users
          </h2>

          <div className="tableScroll">
            <table>
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>XP</th>
                </tr>
              </thead>

              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>
                      {user.username}
                    </td>

                    <td>
                      {user.email}
                    </td>

                    <td>
                      {user.role}
                    </td>

                    <td>
                      {user.points}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </>
  );
}
