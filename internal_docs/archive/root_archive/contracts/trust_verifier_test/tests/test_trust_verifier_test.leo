// The 'test_trust_verifier_test' test program.
import trust_verifier_test.aleo;
program test_trust_verifier_test.aleo {
    @test
    script test_it() {
        let result: u32 = trust_verifier_test.aleo/main(1u32, 2u32);
        assert_eq(result, 3u32);
    }

    @test
    @should_fail
    transition do_nothing() {
        let result: u32 = trust_verifier_test.aleo/main(2u32, 3u32);
        assert_eq(result, 3u32);
    }
}
