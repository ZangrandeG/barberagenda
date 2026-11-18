package br.com.barberagenda.security;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.barberagenda.dto.ErroResponse;
import jakarta.servlet.http.HttpServletResponse;

/** Escreve respostas JSON nos filtros de segurança, que rodam antes dos controllers. */
@Component
public class RespostaJson {

    private final ObjectMapper mapeador;

    public RespostaJson(ObjectMapper mapeador) {
        this.mapeador = mapeador;
    }

    public void erro(HttpServletResponse resposta, HttpStatus status, String mensagem) throws IOException {
        escrever(resposta, status, ErroResponse.de(status.value(), status.getReasonPhrase(), mensagem));
    }

    public void escrever(HttpServletResponse resposta, HttpStatus status, Object corpo) throws IOException {
        resposta.setStatus(status.value());
        resposta.setContentType(MediaType.APPLICATION_JSON_VALUE);
        resposta.setCharacterEncoding(StandardCharsets.UTF_8.name());
        mapeador.writeValue(resposta.getOutputStream(), corpo);
    }
}
