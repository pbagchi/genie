/*
 *
 *  Copyright 2018 Netflix, Inc.
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 *
 */
package com.netflix.genie.agent.execution.process;

import com.netflix.genie.agent.execution.exceptions.JobLaunchException;
import com.netflix.genie.agent.execution.services.KillService;
import org.springframework.context.ApplicationListener;

import javax.annotation.Nullable;
import java.io.File;
import java.util.List;
import java.util.Map;

/**
 * Singleton to manage the subprocess for the actual user job this Agent instance is managing.
 *
 * @author mprimi
 * @author tgianos
 * @since 4.0.0
 */
public interface JobProcessManager extends ApplicationListener<KillService.KillEvent> {

    /**
     * Launch the job process (unless launch was aborted by previous a {@code kill} call).
     *
     * @param jobDirectory         Job directory
     * @param environmentVariables additional environment variables (to merge on top of inherited environment)
     * @param commandArguments     command-line executable and its fixed arguments arguments
     * @param jobArguments         job-specific arguments
     * @param interactive          launch in interactive mode (inherit I/O) or batch (no input, write outputs to files)
     * @param timeout              The optional number of seconds this job is allowed to run before the system will
     *                             kill it
     * @throws JobLaunchException if the job process failed to launch
     */
    void launchProcess(
        File jobDirectory,
        Map<String, String> environmentVariables,
        List<String> commandArguments,
        List<String> jobArguments,
        boolean interactive,
        @Nullable Integer timeout
    ) throws JobLaunchException;

    /**
     * Terminate job process execution (if still running) or prevent it from launching (if not launched yet).
     * Optionally sends SIGINT to the process (unnecessary under certain circumstances. For example,
     * CTRL-C in a terminal session, is already received by the job process, issuing a second one is unneeded).
     *
     * @param source The {@link KillService.KillSource} value representing where this kill request is coming from
     */
    void kill(KillService.KillSource source);

    /**
     * Wait indefinitely for the job process to terminate.
     *
     * @return KILLED, SUCCESSFUL, or FAILED
     * @throws IllegalStateException if the process was not launched
     * @throws InterruptedException  if the calling thread is interrupted while waiting
     */
    JobProcessResult waitFor() throws InterruptedException;
}
