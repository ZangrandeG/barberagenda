package br.com.barberagenda.dto;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import jakarta.validation.Constraint;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import jakarta.validation.Payload;

/** Exige que o número inteiro seja múltiplo de {@link #valor()}. Valores nulos são aceitos. */
@Documented
@Constraint(validatedBy = MultiploDe.Validador.class)
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.RECORD_COMPONENT})
@Retention(RetentionPolicy.RUNTIME)
public @interface MultiploDe {

    int valor();

    String message() default "O valor deve ser múltiplo de {valor}.";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    class Validador implements ConstraintValidator<MultiploDe, Integer> {

        private int divisor;

        @Override
        public void initialize(MultiploDe anotacao) {
            this.divisor = anotacao.valor();
        }

        @Override
        public boolean isValid(Integer numero, ConstraintValidatorContext contexto) {
            return numero == null || numero % divisor == 0;
        }
    }
}
