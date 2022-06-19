import { Container } from "reactstrap";

export default function Footer() {
  return (
    <footer className="footer bg-light py-4">
      <Container className="text-center text-muted">
        &copy; {`${new Date().getFullYear()} `}
        <a href="https://kvdomingo.xyz" target="_blank" rel="noopener noreferrer">
          Kenneth V. Domingo
        </a>
      </Container>
    </footer>
  );
}
