CREATE DATABASE coding_challenge;



CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job VARCHAR(255) NOT NULL
);

CREATE TABLE hired_employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    department_id INT REFERENCES departments(id),
    job_id INT REFERENCES jobs(id)
);
