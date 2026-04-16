import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from './Navbar.module.css';

export default function Navbar() {
  const { pathname } = useLocation();

  return (
    <nav className={styles.nav}>
      <Link to="/" className={styles.logo}>
        <span className={styles.logoIcon}>◈</span>
        <span className={styles.logoText}>Voxemo</span>
      </Link>

      <div className={styles.links}>
        <Link to="/" className={`${styles.link} ${pathname === '/' ? styles.active : ''}`}>
          Home
        </Link>
        <Link to="/predict" className={`${styles.link} ${pathname === '/predict' ? styles.active : ''}`}>
          Analyze
        </Link>
        <Link to="/history" className={`${styles.link} ${pathname === '/history' ? styles.active : ''}`}>
          History
        </Link>
        <a
          href="https://github.com"
          target="_blank"
          rel="noopener noreferrer"
          className={styles.link}
        >
          GitHub
        </a>
      </div>
    </nav>
  );
}
