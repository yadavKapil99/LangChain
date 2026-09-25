// ===== 1. Regular function =====
function greet(name = "Guest") {
  return `Hello, ${name}!`;
}

// ===== 2. Arrow functions =====
const add = (a, b) => a + b;
const square = (n) => n * n;

// ===== 3. Function with rest parameters =====
function sumAll(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}

// ===== 4. Higher-order function (takes a function as an argument) =====
function applyToAll(arr, fn) {
  return arr.map(fn);
}

// ===== 5. Closure (function that returns a function) =====
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getValue: () => count,
  };
}

// ===== 6. Recursive function =====
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// ===== 7. Async function with error handling =====
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchUser(id) {
  try {
    await delay(500); // simulate network delay
    if (id <= 0) throw new Error("Invalid user ID");
    return { id, name: `User${id}`, email: `user${id}@example.com` };
  } catch (err) {
    console.error("Error:", err.message);
    return null;
  }
}

// ===== 8. Generator function =====
function* fibonacci(limit) {
  let [a, b] = [0, 1];
  for (let i = 0; i < limit; i++) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// ===== 9. Utility: debounce =====
function debounce(fn, wait) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}

// ===== 10. Class with methods =====
class Calculator {
  constructor() {
    this.history = [];
  }

  calculate(a, operator, b) {
    const ops = {
      "+": (x, y) => x + y,
      "-": (x, y) => x - y,
      "*": (x, y) => x * y,
      "/": (x, y) => (y !== 0 ? x / y : NaN),
    };
    const result = ops[operator]?.(a, b) ?? NaN;
    this.history.push(`${a} ${operator} ${b} = ${result}`);
    return result;
  }

  showHistory() {
    this.history.forEach((entry, i) => console.log(`${i + 1}. ${entry}`));
  }
}

// ===== Main: run everything =====
async function main() {
  console.log(greet("Kapil"));                        // Hello, Kapil!
  console.log("add:", add(5, 3));                     // 8
  console.log("sumAll:", sumAll(1, 2, 3, 4, 5));      // 15
  console.log("squares:", applyToAll([1, 2, 3], square)); // [1, 4, 9]
  console.log("factorial(5):", factorial(5));         // 120

  const counter = createCounter();
  counter.increment();
  counter.increment();
  counter.decrement();
  console.log("counter:", counter.getValue());        // 1

  console.log("fibonacci:", [...fibonacci(10)]);      // [0,1,1,2,3,5,8,13,21,34]

  const calc = new Calculator();
  calc.calculate(10, "+", 5);
  calc.calculate(20, "/", 4);
  calc.calculate(7, "*", 6);
  calc.showHistory();

  const user = await fetchUser(1);
  console.log("user:", user);
  await fetchUser(-1);                                // logs an error, returns null

  const log = debounce((msg) => console.log("debounced:", msg), 300);
  log("a");
  log("b");
  log("c");                                           // only "c" prints
}

main();
