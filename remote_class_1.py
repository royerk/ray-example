import ray
from datetime import datetime
import argparse


@ray.remote
class Follower:
    def __init__(self, _id):
        self.id = _id

    def fibonacci(self, n):
        """
        This function should be slow for proper demonstration.
        """
        if n == 1 or n == 2:
            return 1
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    def follower_fibonacci(self, n):
        """
        Wrapper around call to fibonacci.
        @param n: parameter to fibonacci
        @return n requested, fibonacci(n), follower id
        """
        return n, self.fibonacci(n), self.id


class Leader:
    def __init__(self, n_followers):
        """
        For simplicity sake, n cpu == n followers.
        @param n_followers: number of followers
        """
        ray.init(num_cpus=n_followers)
        self.followers = [Follower.remote(i) for i in range(n_followers)]

    def get_fibonacci_values(self, start_n=20, end_n=30, force_async=False):
        """
        Ask followers to compute fibonacci values. Here followers are
        idle after submitting their answer.
        @param start_n: first value to compute
        @param end_n: last value to compute
        """
        received_answers = 0
        expected_answers = end_n - start_n
        print("{} answers expected".format(expected_answers))

        fibonacci_list = []
        # initialize by asking followers to compute first values
        for follower in self.followers:
            fibonacci_list.append(follower.follower_fibonacci.remote(start_n))
            start_n += 1

        # here the stop condition is reached when we get the number of expected answer
        # another option is to have while True and an if condition: run more else: break
        while received_answers < expected_answers:
            # collect first result as soon as it's possible
            # keep track in the list of the other results
            done_id, fibonacci_list = ray.wait(fibonacci_list)

            # parse answer from follower and print
            n_fib, answer_fibonacci, follower_id = ray.get(done_id)[0]
            received_answers += 1
            start_n += 1
            print(
                "Follower {}: fib({})={}, received answers: {}".format(
                    follower_id, n_fib, answer_fibonacci, received_answers
                )
            )

            # ask the follower for another value
            if start_n <= end_n:
                weird_factor = 0
                if force_async:
                    # this is a trick to observe the asynchronous behavior
                    # some followers will be asked for higher numbers
                    # this means: follower 0 should show more often
                    weird_factor = (follower_id + 1) * 4
                print(
                    "Requesting fib({}) from follower: {}".format(
                        start_n + weird_factor, follower_id
                    )
                )
                fibonacci_list.extend(
                    [
                        self.followers[follower_id].follower_fibonacci.remote(
                            start_n + weird_factor
                        )
                    ]
                )


def main(n_followers=2, start_n=30, end_n=38, force_async=False):
    start_date = datetime.now()
    leader = Leader(n_followers)

    leader.get_fibonacci_values(start_n, end_n, force_async)

    end_date = datetime.now()

    print(
        "{} followers, duration: :{}".format(
            len(leader.followers), end_date - start_date
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a leader and followers to get fibonacci values."
    )
    parser.add_argument(
        "--followers",
        default=2,
        type=int,
        help="Choose number of followers (== number of cpu).",
    )
    parser.add_argument(
        "--start", default=20, type=int, help="Start getting fibonacci at this value",
    )
    parser.add_argument(
        "--end", default=30, type=int, help="Last value to compute",
    )
    parser.add_argument(
        "--async",
        default=False,
        help="Uneven load on followers to illustrate async better",
        action="store_true",
    )
    args = parser.parse_args()
    print(args)

    main(
        n_followers=args.followers,
        start_n=args.start,
        end_n=args.end,
        force_async=args.async,
    )
