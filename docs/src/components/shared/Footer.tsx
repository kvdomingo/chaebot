export default function Footer() {
  return (
    <footer className="footer py-8">
      <div className="container text-center text-neutral-500">
        &copy; 2020-{`${new Date().getFullYear()} `}
        <a
          href="https://kvd.studio"
          target="_blank"
          rel="noopener noreferrer"
          className="text-sky-500"
        >
          KVD Studio
        </a>
      </div>
    </footer>
  );
}
