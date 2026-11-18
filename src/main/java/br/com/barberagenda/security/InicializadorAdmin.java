package br.com.barberagenda.security;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.annotation.Order;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import br.com.barberagenda.model.Usuario;
import br.com.barberagenda.repository.UsuarioRepository;

/**
 * Cria o administrador na inicialização, se ainda não existir.
 * Login e senha vêm das propriedades barberagenda.admin.* (variáveis ADMIN_LOGIN e ADMIN_SENHA).
 * O valor padrão (admin/admin123) é uma credencial FICTÍCIA, apenas para desenvolvimento e testes.
 */
@Component
@Order(1)
public class InicializadorAdmin implements ApplicationRunner {

    private static final Logger LOG = LoggerFactory.getLogger(InicializadorAdmin.class);

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder codificadorSenha;
    private final String login;
    private final String senha;

    public InicializadorAdmin(UsuarioRepository usuarioRepository, PasswordEncoder codificadorSenha,
                              @Value("${barberagenda.admin.login}") String login,
                              @Value("${barberagenda.admin.senha}") String senha) {
        this.usuarioRepository = usuarioRepository;
        this.codificadorSenha = codificadorSenha;
        this.login = login;
        this.senha = senha;
    }

    @Override
    @Transactional
    public void run(ApplicationArguments args) {
        if (usuarioRepository.findByLogin(login).isEmpty()) {
            usuarioRepository.save(new Usuario(login, codificadorSenha.encode(senha), "ADMIN"));
            LOG.info("Usuário administrador '{}' criado.", login);
        }
    }
}
