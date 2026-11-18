package br.com.barberagenda.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;
import org.springframework.security.web.csrf.CsrfException;
import org.springframework.security.web.csrf.CsrfFilter;
import org.springframework.security.web.util.matcher.AndRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;

import br.com.barberagenda.dto.SessaoResponse;
import jakarta.servlet.http.HttpServletRequest;

/**
 * Segurança da aplicação (RN-11).
 * <ul>
 *   <li>Área pública: páginas do cliente e API de cadastro/agendamento.</li>
 *   <li>Área administrativa: páginas /admin/** (login por formulário, sessão) e API /api/admin/**
 *       (sessão ou HTTP Basic). Sem credenciais a API responde 401; com perfil inadequado ou
 *       token CSRF inválido, 403.</li>
 *   <li>Listagem e consulta de clientes por id (GET /api/clientes/**) também exigem administrador,
 *       pois expõem dados pessoais.</li>
 *   <li>A restauração de dados (/api/dev/**, só existe nos perfis dev e test) apaga registros e por
 *       isso também exige administrador e segue a mesma regra de CSRF da área administrativa.</li>
 *   <li>CSRF: exigido nas requisições de alteração da área administrativa feitas com sessão
 *       (navegador). Requisições com cabeçalho Authorization (HTTP Basic, ex.: Postman) não usam
 *       cookie de sessão e por isso dispensam o token.</li>
 * </ul>
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private static final String PAGINA_LOGIN = "/admin/login.html";

    @Bean
    public PasswordEncoder codificadorSenha() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain cadeiaFiltros(HttpSecurity http, RespostaJson json) throws Exception {
        RequestMatcher api = req -> caminho(req).startsWith("/api/");
        RequestMatcher areaAdministrativa = req -> {
            String caminho = caminho(req);
            return caminho.startsWith("/api/admin/") || caminho.startsWith("/admin/")
                    || caminho.startsWith("/api/dev/");
        };
        RequestMatcher semCabecalhoAuthorization = req -> req.getHeader(HttpHeaders.AUTHORIZATION) == null;
        RequestMatcher exigeCsrf = new AndRequestMatcher(
                CsrfFilter.DEFAULT_CSRF_MATCHER, areaAdministrativa, semCabecalhoAuthorization);

        AuthenticationEntryPoint pontoEntrada = (req, res, ex) -> {
            if (api.matches(req)) {
                json.erro(res, HttpStatus.UNAUTHORIZED, "Autenticação necessária.");
            } else {
                res.sendRedirect(req.getContextPath() + PAGINA_LOGIN);
            }
        };
        AccessDeniedHandler acessoNegado = (req, res, ex) -> json.erro(res, HttpStatus.FORBIDDEN,
                ex instanceof CsrfException ? "Token CSRF ausente ou inválido." : "Acesso negado.");

        http
            .csrf(csrf -> csrf
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
                .csrfTokenRequestHandler(new SpaCsrfTokenRequestHandler())
                .requireCsrfProtectionMatcher(exigeCsrf))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(PAGINA_LOGIN, "/admin/login").permitAll()
                .requestMatchers("/admin/**", "/api/admin/**", "/api/dev/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.GET, "/api/clientes", "/api/clientes/**").hasRole("ADMIN")
                .anyRequest().permitAll())
            .formLogin(form -> form
                .loginPage(PAGINA_LOGIN)
                .loginProcessingUrl("/admin/login")
                .successHandler((req, res, autenticacao) ->
                        json.escrever(res, HttpStatus.OK, new SessaoResponse(autenticacao.getName())))
                .failureHandler((req, res, ex) ->
                        json.erro(res, HttpStatus.UNAUTHORIZED, "Usuário ou senha inválidos."))
                .permitAll())
            .logout(logout -> logout
                .logoutUrl("/admin/logout")
                .logoutSuccessHandler((req, res, autenticacao) -> res.setStatus(HttpStatus.NO_CONTENT.value())))
            .httpBasic(basic -> basic.authenticationEntryPoint(pontoEntrada))
            .exceptionHandling(excecoes -> excecoes
                .authenticationEntryPoint(pontoEntrada)
                .accessDeniedHandler(acessoNegado));

        return http.build();
    }

    private static String caminho(HttpServletRequest req) {
        return req.getRequestURI().substring(req.getContextPath().length());
    }
}
