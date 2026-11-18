package br.com.barberagenda.security;

import java.util.function.Supplier;

import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.security.web.csrf.CsrfTokenRequestAttributeHandler;
import org.springframework.security.web.csrf.CsrfTokenRequestHandler;
import org.springframework.security.web.csrf.XorCsrfTokenRequestAttributeHandler;
import org.springframework.util.StringUtils;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Tratamento de token CSRF para páginas que usam JavaScript (fetch):
 * o token é gravado no cookie XSRF-TOKEN e o JavaScript o devolve no cabeçalho X-XSRF-TOKEN.
 * Baseado na recomendação da documentação do Spring Security para aplicações de página única.
 */
final class SpaCsrfTokenRequestHandler implements CsrfTokenRequestHandler {

    private final CsrfTokenRequestHandler simples = new CsrfTokenRequestAttributeHandler();
    private final CsrfTokenRequestHandler xor = new XorCsrfTokenRequestAttributeHandler();

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response, Supplier<CsrfToken> csrfToken) {
        this.xor.handle(request, response, csrfToken);
        // Força a geração do token para que o cookie XSRF-TOKEN seja enviado ao navegador.
        csrfToken.get();
    }

    @Override
    public String resolveCsrfTokenValue(HttpServletRequest request, CsrfToken csrfToken) {
        String valorCabecalho = request.getHeader(csrfToken.getHeaderName());
        return (StringUtils.hasText(valorCabecalho) ? this.simples : this.xor)
                .resolveCsrfTokenValue(request, csrfToken);
    }
}
