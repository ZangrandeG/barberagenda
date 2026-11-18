package br.com.barberagenda.config;

import java.time.Clock;
import java.time.ZoneId;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Disponibiliza um {@link Clock} injetável. As regras que dependem de data e hora
 * consultam este relógio, o que permite fixar o "agora" nos testes automatizados.
 */
@Configuration
public class RelogioConfig {

    @Bean
    public Clock relogio(@Value("${barberagenda.fuso-horario}") String fusoHorario) {
        return Clock.system(ZoneId.of(fusoHorario));
    }
}
