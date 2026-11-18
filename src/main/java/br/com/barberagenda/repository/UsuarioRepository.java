package br.com.barberagenda.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.barberagenda.model.Usuario;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {

    Optional<Usuario> findByLogin(String login);
}
